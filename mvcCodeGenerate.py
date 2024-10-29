# 导入冰激凌
# 导入解析参数的库
import argparse
import os
from pathlib import Path

# 导入 mysql 模块
import pymysql
from icecream import ic

Java_Package_Prefix = "src/main/java/"

DO_Sub_Path = "domain/dao"
DO_Sub_Package = "domain.dao"
Dto_Sub_Path = "domain/dto"
Dto_Sub_Package = "domain.dto"
Vo_Sub_Path = "domain/vo"
Vo_Sub_Package = "domain.vo"
Data_Transform_Sub_Path = "domain/data_transform"
Data_Transform_Sub_Package = "domain.data_transform"
Mapper_Sub_Path = "repository/mapper"
Mapper_Sub_Package = "repository.mapper"
Service_Sub_Path = "service"
Service_Sub_Package = "service"
Controller_Sub_Path = "controller"
Controller_Sub_Package = "controller"


# 声明枚举, 表示数据类型
class DataType:
    INT = "int"
    VARCHAR = "varchar"
    TIMESTAMP = "timestamp"
    DATETIME = "datetime"
    TEXT = "text"


class TableField:
    def __init__(self, name: str, type: DataType, is_auto_increment: bool):
        self.name = name
        self.type = type
        self.is_auto_increment = is_auto_increment

    def __str__(self):
        return f"字段名: {self.name}, 字段类型: {self.type}, 是否自增: {self.is_auto_increment}"


# TableInfo 表示表的信息, 构造方法传入表的名称和字段的列表
class TableInfo:
    def __init__(self, name: str, field_list: list[TableField]):
        self.name = name
        self.field_list = field_list

    def __str__(self):
        return f"表名: {self.name}, 字段列表: {self.field_list}"


def full_dto_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Dto_Sub_Package}.{to_java_class_name(name = name)}Dto"


def full_insert_dto_package_name(package_name: str, name: str) -> str:
    return (
        f"{package_name}.{Dto_Sub_Package}.{to_java_class_name(name = name)}InsertDto"
    )


def full_vo_req_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Vo_Sub_Package}.{to_java_class_name(name = name)}VoReq"


def full_vo_res_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Vo_Sub_Package}.{to_java_class_name(name = name)}VoRes"


def full_mapper_package_name(package_name: str, name: str) -> str:
    return (
        f"{package_name}.{Mapper_Sub_Package}.{to_java_class_name(name = name)}Mapper"
    )


def full_service_package_name(package_name: str, name: str) -> str:
    return (
        f"{package_name}.{Service_Sub_Package}.{to_java_class_name(name = name)}Service"
    )


def full_method_to_insert_dto_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Data_Transform_Sub_Package}.toInsertDto"


def full_method_to_do_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Data_Transform_Sub_Package}.toDo"


def full_method_do_to_dto_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Data_Transform_Sub_Package}.toDto"


def full_method_to_vo_res_package_name(package_name: str, name: str) -> str:
    return f"{package_name}.{Data_Transform_Sub_Package}.toVoRes"


def mysql_data_type_to_java_data_type(mysql_data_type: DataType) -> str:
    if mysql_data_type == DataType.INT:
        return "Integer"
    elif mysql_data_type == DataType.VARCHAR:
        return "String"
    elif mysql_data_type == DataType.TIMESTAMP:
        return "Date"
    elif mysql_data_type == DataType.DATETIME:
        return "Date"
    elif mysql_data_type == DataType.TEXT:
        return "String"
    else:
        raise Exception(f"不支持的数据类型: {mysql_data_type}")


def mysql_data_type_to_kolin_data_type(mysql_data_type: DataType) -> str:
    if mysql_data_type == DataType.INT:
        return "Int"
    elif mysql_data_type == DataType.VARCHAR:
        return "String"
    elif mysql_data_type == DataType.TIMESTAMP:
        return "Date"
    elif mysql_data_type == DataType.DATETIME:
        return "Date"
    elif mysql_data_type == DataType.TEXT:
        return "String"
    else:
        raise Exception(f"不支持的数据类型: {mysql_data_type}")


def create_args():
    # 解析参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-fc",
        "--force_cover",
        action="store_true",
        help="是否强制覆盖",
    )
    parser.add_argument(
        "-mh",
        "--mysql_host",
        type=str,
        required=True,
        help="数据库的地址",
    )
    parser.add_argument(
        "-mp",
        "--mysql_port",
        type=int,
        required=True,
        help="数据库的端口",
    )
    parser.add_argument(
        "-mun",
        "--mysql_user_name",
        type=str,
        required=True,
        help="数据库的用户名",
    )
    parser.add_argument(
        "-mpw",
        "--mysql_password",
        type=str,
        required=True,
        help="数据库的密码",
    )
    parser.add_argument(
        "-dn",
        "--database_name",
        type=str,
        required=True,
        help="数据库的名字",
    )
    parser.add_argument(
        "-tn",
        "--table_name",
        type=str,
        required=True,
        help="表的名字",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=1,
        required=False,
        help="版本号",
    )

    args = parser.parse_args()
    return args


# 下划线转驼峰
def to_java_class_name(name: str) -> str:
    name = name.lower()
    name_list = name.split("_")
    java_name = ""
    for item in name_list:
        java_name += item.capitalize()
    return java_name


def to_java_attr_name(name: str) -> str:
    # 首字母小写
    class_name = to_java_class_name(name=name)
    return class_name[0].lower() + class_name[1:]


def connect_mysql_and_get_table_structure(args) -> TableInfo:
    mysql_host = args.mysql_host
    mysql_port = args.mysql_port
    mysql_user_name = args.mysql_user_name
    mysql_password = args.mysql_password
    database_name = args.database_name
    table_name = args.table_name

    ic(mysql_host)
    ic(mysql_port)
    ic(mysql_user_name)
    ic(mysql_password)
    ic(database_name)
    ic(table_name)

    # 连接数据库
    conn = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user_name,
        password=mysql_password,
        database=database_name,
    )
    ic(conn)

    # 获取表结构的信息
    cursor = conn.cursor()
    sql = f"desc {table_name}"
    cursor.execute(sql)
    table_structure = cursor.fetchall()
    # 关闭数据库连接
    conn.close()
    ic(table_structure)

    # 提取表字段的信息
    field_list = []
    for item in table_structure:
        ic(item)
        mysql_field_type = item[1]

        if mysql_field_type.startswith("int"):
            field_type = DataType.INT
        elif mysql_field_type.startswith("varchar"):
            field_type = DataType.VARCHAR
        elif mysql_field_type.startswith("timestamp"):
            field_type = DataType.TIMESTAMP
        else:
            raise Exception(f"不支持的字段类型: {mysql_field_type}")

        table_field = TableField(
            name=item[0],
            type=field_type,
            is_auto_increment="auto_increment" in item[5],
        )

        ic(f"table_field: name = {table_field.name}, type = {table_field.type}")
        field_list.append(
            table_field,
        )

    return TableInfo(
        name=table_name,
        field_list=field_list,
    )


def get_package_name(current_path: str) -> str:
    index = current_path.find(Java_Package_Prefix)
    if index == -1:
        raise Exception("当前路径不是 Java 项目的路径")

    package_name = current_path[index + len(Java_Package_Prefix) :].replace("/", ".")
    return package_name


def createDaoEntityClass(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)

    target_folder = Path(current_path) / DO_Sub_Path
    mapper_file_name = to_java_class_name(name=table_info.name) + "Do.java"
    target_file = target_folder / mapper_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    # 文件内容准备
    content_list: list[str] = []
    content_list.append(f"package {package_name}.{DO_Sub_Package};")
    content_list.append("")
    content_list.append("import com.baomidou.mybatisplus.annotation.IdType;")
    content_list.append("import com.baomidou.mybatisplus.annotation.TableId;")
    content_list.append("import com.baomidou.mybatisplus.annotation.TableName;")
    content_list.append("")
    content_list.append("import java.util.Date;")
    content_list.append("")
    content_list.append(f'@TableName("{table_info.name}")')
    content_list.append(
        f"public class {to_java_class_name(name=table_info.name)}Do " + "{"
    )
    content_list.append("")
    # 遍历字段, 添加属性
    for field in table_info.field_list:
        if field.is_auto_increment:
            content_list.append(
                f"\t@TableId(type = IdType.AUTO)",
            )
        content_list.append(
            f"\tprivate {mysql_data_type_to_java_data_type(mysql_data_type = field.type)} {to_java_attr_name(name = field.name)};"
        )
        content_list.append("")
    # 遍历字段, 添加 getter 和 setter
    for field in table_info.field_list:
        content_list.append(
            f"\tpublic {mysql_data_type_to_java_data_type(mysql_data_type = field.type)} get{to_java_class_name(name = field.name)}() "
            + "{"
        )
        content_list.append(f"\t\treturn {to_java_attr_name(name = field.name)};")
        content_list.append("\t}")
        content_list.append("")
        content_list.append(
            f"\tpublic void set{to_java_class_name(name = field.name)}({mysql_data_type_to_java_data_type(mysql_data_type = field.type)} {to_java_attr_name(name = field.name)}) "
            + "{"
        )
        content_list.append(
            f"\t\tthis.{to_java_attr_name(name = field.name)} = {to_java_attr_name(name = field.name)};"
        )
        content_list.append("\t}")
        content_list.append("")

    content_list.append("}")
    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]
    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def createDtoEntityClass(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)

    target_folder = Path(current_path) / Dto_Sub_Path
    dto_file_name = to_java_class_name(name=table_info.name) + "Dto.kt"
    target_file = target_folder / dto_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    content_list = []
    content_list.append(f"package {package_name}.{Dto_Sub_Package}")
    content_list.append("")
    content_list.append("import java.util.Date")
    content_list.append("")
    content_list.append(f"class {to_java_class_name(name = table_info.name)}InsertDto(")
    # 遍历字段, 添加属性
    for field in table_info.field_list:
        if field.is_auto_increment:
            continue
        content_list.append(
            f"\tval {to_java_attr_name(name = field.name)}: {mysql_data_type_to_kolin_data_type(mysql_data_type = field.type)},"
        )
    content_list.append(")")
    content_list.append("")
    content_list.append(f"class {to_java_class_name(name = table_info.name)}Dto(")
    # 遍历字段, 添加属性
    for field in table_info.field_list:
        content_list.append(
            f"\tval {to_java_attr_name(name = field.name)}: {mysql_data_type_to_kolin_data_type(mysql_data_type = field.type)},"
        )
    content_list.append(")")
    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]
    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def createVoEntityClass(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)

    target_folder = Path(current_path) / Vo_Sub_Path
    dto_file_name = to_java_class_name(name=table_info.name) + "Vo.kt"
    target_file = target_folder / dto_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    content_list = []
    content_list.append(f"package {package_name}.{Vo_Sub_Package}")
    content_list.append("")
    content_list.append("import java.util.Date")
    content_list.append("")
    content_list.append(f"class {to_java_class_name(name = table_info.name)}VoReq(")
    # 遍历字段, 添加属性
    for field in table_info.field_list:
        if field.is_auto_increment:
            continue
        content_list.append(
            f"\tval {to_java_attr_name(name = field.name)}: {mysql_data_type_to_kolin_data_type(mysql_data_type = field.type)},"
        )
    content_list.append(")")
    content_list.append("")
    content_list.append(f"class {to_java_class_name(name = table_info.name)}VoRes(")
    # 遍历字段, 添加属性
    for field in table_info.field_list:
        content_list.append(
            f"\tval {to_java_attr_name(name = field.name)}: {mysql_data_type_to_kolin_data_type(mysql_data_type = field.type)},"
        )
    content_list.append(")")
    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]
    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def create_data_transform_file(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)
    class_name = to_java_class_name(name=table_info.name)

    target_folder = Path(current_path) / Data_Transform_Sub_Path
    dto_file_name = class_name + "TF.kt"
    target_file = target_folder / dto_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    content_list = []

    content_list.append(f"package {package_name}.{Data_Transform_Sub_Package}")
    # 导入包
    content_list.append(f"import {package_name}.{DO_Sub_Package}.{class_name}Do")
    content_list.append(
        f"import {full_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {package_name}.{Dto_Sub_Package}.{class_name}InsertDto",
    )
    content_list.append(
        f"import {package_name}.{Vo_Sub_Package}.{class_name}VoReq",
    )
    content_list.append(
        f"import {package_name}.{Vo_Sub_Package}.{class_name}VoRes",
    )

    content_list.append("")
    # 生成 vo to insertDto 的扩展方法
    content_list.append(
        f"fun {class_name}VoReq.toInsertDto(): {class_name}InsertDto " + "{",
    )
    content_list.append("\tval target = this")
    content_list.append(f"\treturn {class_name}InsertDto(")
    for field in table_info.field_list:
        if field.is_auto_increment:
            continue
        content_list.append(
            f"\t\t{to_java_attr_name(name = field.name)} = target.{to_java_attr_name(name = field.name)},"
        )
    content_list.append("\t)")
    content_list.append("}")

    content_list.append("")
    # 生成 insert dto to do 的扩展方法
    content_list.append(
        f"fun {class_name}InsertDto.toDo(): {class_name}Do " + "{",
    )
    content_list.append("\tval target = this")
    content_list.append(f"\treturn {class_name}Do().apply" + "{")
    for field in table_info.field_list:
        if field.is_auto_increment:
            continue
        content_list.append(
            f"\t\tthis.{to_java_attr_name(name = field.name)} = target.{to_java_attr_name(name = field.name)}"
        )
    content_list.append("\t}")
    content_list.append("}")

    content_list.append("")

    content_list.append("")
    # 生成 dto to do 的扩展方法
    content_list.append(
        f"fun {class_name}Dto.toDo(): {class_name}Do " + "{",
    )
    content_list.append("\tval target = this")
    content_list.append(f"\treturn {class_name}Do().apply" + "{")
    for field in table_info.field_list:
        content_list.append(
            f"\t\tthis.{to_java_attr_name(name = field.name)} = target.{to_java_attr_name(name = field.name)}"
        )
    content_list.append("\t}")
    content_list.append("}")

    content_list.append("")

    # 生成 do to dto 的扩展方法
    content_list.append(
        f"fun {class_name}Do.toDto(): {class_name}Dto " + "{",
    )
    content_list.append("\tval target = this")
    content_list.append(f"\treturn {class_name}Dto(")
    for field in table_info.field_list:
        content_list.append(
            f"\t\t{to_java_attr_name(name = field.name)} = target.{to_java_attr_name(name = field.name)},"
        )
    content_list.append("\t)")
    content_list.append("}")

    content_list.append("")

    # 生成 dto to vo res 的扩展方法
    content_list.append(
        f"fun {class_name}Dto.toVoRes(): {class_name}VoRes " + "{",
    )
    content_list.append("\tval target = this")
    content_list.append(f"\treturn {class_name}VoRes(")
    for field in table_info.field_list:
        content_list.append(
            f"\t\t{to_java_attr_name(name = field.name)} = target.{to_java_attr_name(name = field.name)},"
        )
    content_list.append("\t)")
    content_list.append("}")

    content_list = [item + "\n" for item in content_list]
    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def createMapper(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)

    target_folder = Path(current_path) / Mapper_Sub_Path
    mapper_file_name = to_java_class_name(name=table_info.name) + "Mapper.kt"
    target_file = target_folder / mapper_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    class_name = to_java_class_name(name=table_info.name)
    # 文件内容准备
    content_list: list[str] = []
    content_list.append(f"package {package_name}.{Mapper_Sub_Package}")
    content_list.append("")
    content_list.append("import com.baomidou.mybatisplus.core.mapper.BaseMapper")
    content_list.append(f"import {package_name}.{DO_Sub_Package}.{class_name}Do")
    content_list.append("import org.apache.ibatis.annotations.Mapper")
    content_list.append("")
    content_list.append("@Mapper")
    content_list.append(f"interface {class_name}Mapper : BaseMapper<{class_name}Do>")
    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]

    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def createService(
    current_path: str,
    table_info: TableInfo,
    force_cover: bool = False,
):
    # 寻找表的字段列表中的主键ID
    field_list = table_info.field_list
    primary_key_field = None
    for field in field_list:
        if field.is_auto_increment:
            primary_key_field = field
            break
    if primary_key_field is None:
        raise Exception(f"表: {table_info.name} 没有主键")
    package_name = get_package_name(current_path=current_path)
    attr_name = to_java_attr_name(name=table_info.name)
    class_name = to_java_class_name(name=table_info.name)

    target_folder = Path(current_path) / Service_Sub_Path
    service_file_name = to_java_class_name(name=table_info.name) + "Service.kt"
    target_file = target_folder / service_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    # 文件内容准备
    content_list: list[str] = []
    content_list.append(f"package {package_name}.{Service_Sub_Package}")
    content_list.append("")
    content_list.append(
        f"import {full_method_to_do_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_method_do_to_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_insert_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_mapper_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append("import org.springframework.beans.factory.annotation.Autowired")
    content_list.append("import org.springframework.stereotype.Service")
    content_list.append(
        "import org.springframework.transaction.annotation.Transactional"
    )
    content_list.append("")
    content_list.append("@Service")
    content_list.append(f"class {class_name}Service " + "{")
    content_list.append("")
    content_list.append("\t@Autowired")
    content_list.append(f"\tlateinit var {attr_name}Mapper: {class_name}Mapper")
    content_list.append("")
    content_list.append("\t@Transactional")
    content_list.append(
        f"\tfun saveAndQuery(target: {class_name}InsertDto): {class_name}Dto " + "{"
    )
    content_list.append(f"\t\tval targetDo = target.toDo()")
    content_list.append(f"\t\t{attr_name}Mapper.insert(targetDo)")
    content_list.append(
        f"\t\treturn {attr_name}Mapper.selectById(targetDo.{to_java_attr_name(name = primary_key_field.name)}).toDto()"
    )
    content_list.append("\t}")
    content_list.append("")
    content_list.append("\t@Transactional")
    content_list.append("\tfun deleteById(id: Int) " + "{")
    content_list.append(f"\t\t{attr_name}Mapper.deleteById(id)")
    content_list.append("\t}")
    content_list.append("")
    content_list.append("\t@Transactional")
    content_list.append(f"\tfun update(target: {class_name}Dto) " + "{")
    content_list.append(f"\t\t {attr_name}Mapper.updateById(target.toDo())")
    content_list.append("\t}")
    content_list.append("")
    content_list.append("\t@Transactional")
    content_list.append(f"\tfun selectById(id: Int): {class_name}Dto? " + "{")
    content_list.append(f"\t\treturn {attr_name}Mapper.selectById(id)?.toDto()")
    content_list.append("\t}")
    content_list.append("")
    content_list.append("}")
    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]

    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def createController(
    current_path: str,
    table_info: TableInfo,
    version: int,
    force_cover: bool = False,
):
    package_name = get_package_name(current_path=current_path)
    attr_name = to_java_attr_name(name=table_info.name)
    class_name = to_java_class_name(name=table_info.name)

    target_folder = Path(current_path) / Controller_Sub_Path
    service_file_name = (
        to_java_class_name(name=table_info.name) + f"Controller{version}.kt"
    )
    target_file = target_folder / service_file_name

    # 创建文件夹
    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    if force_cover:  # 如果强制覆盖, 则删除文件
        if target_file.exists():
            target_file.unlink()

    # 创建文件
    if target_file.exists():
        raise Exception(f"文件: {target_file} 已经存在了")

    # 文件内容准备
    content_list: list[str] = []
    content_list.append(f"package {package_name}.{Controller_Sub_Package}")
    content_list.append("")
    content_list.append(
        f"import {full_method_to_vo_res_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_method_to_do_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_method_to_insert_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_method_do_to_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_insert_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_service_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_dto_package_name(package_name=package_name,name=table_info.name)}",
    )
    content_list.append(
        f"import {full_vo_req_package_name(package_name=package_name,name=table_info.name)}"
    )
    content_list.append(
        f"import {full_vo_res_package_name(package_name=package_name,name=table_info.name)}"
    )
    content_list.append("import com.xiaojinzi.tallyserver.domain.vo.ResultVoRes")
    content_list.append("import org.springframework.beans.factory.annotation.Autowired")
    content_list.append("import org.springframework.web.bind.annotation.*")
    content_list.append(
        "import com.xiaojinzi.tallyserver.domain.vo.EmptySuccessResultVoRes"
    )
    content_list.append(
        "import com.xiaojinzi.tallyserver.domain.vo.EmptySuccessResultVoResIns"
    )
    content_list.append("import com.xiaojinzi.tallyserver.anno.FormatResponse")
    content_list.append("")
    content_list.append("@RestController")
    content_list.append(f"class {class_name}Controller " + "{")
    content_list.append("")
    content_list.append("\t@Autowired")
    content_list.append(f"\tlateinit var {attr_name}Service: {class_name}Service")

    content_list.append("")
    content_list.append(f"\t@FormatResponse")
    content_list.append(f'\t@PostMapping("v{version}/{attr_name}")')
    content_list.append(
        f"\tfun add(req: {class_name}VoReq): ResultVoRes<{class_name}VoRes> " + "{"
    )
    content_list.append(f"\t\treturn ResultVoRes.success(")
    content_list.append(f"\t\t\tt = {attr_name}Service.saveAndQuery(")
    content_list.append("\t\t\t\ttarget = req.toInsertDto()")
    content_list.append("\t\t\t).toVoRes()")
    content_list.append("\t\t)")
    content_list.append("\t}")

    content_list.append("")
    content_list.append(f"\t@FormatResponse")
    content_list.append(f'\t@DeleteMapping("v{version}/{attr_name}/' + '{id}")')
    content_list.append(
        f"\tfun delete(@PathVariable id: Int,): EmptySuccessResultVoRes " + "{"
    )
    content_list.append(f"\t\t{attr_name}Service.deleteById(id = id)")
    content_list.append(f"\t\treturn EmptySuccessResultVoResIns")
    content_list.append("\t}")
    content_list.append("")

    content_list.append(f"\t@FormatResponse")
    content_list.append(f'\t@GetMapping("v{version}/{attr_name}/' + '{id}")')
    content_list.append(
        f"\tfun selectById(@PathVariable id: Int): ResultVoRes<{class_name}VoRes?> "
        + "{"
    )
    content_list.append("\t\treturn ResultVoRes.success(")
    content_list.append(f"\t\t\tt = {attr_name}Service.selectById(id = id)?.toVoRes()")
    content_list.append("\t\t)")
    content_list.append("\t}")

    content_list.append("")
    content_list.append("}")

    # 每一行增加一个换行
    content_list = [item + "\n" for item in content_list]

    # 创建文件输出流, 进行内容的输出
    with open(target_file, "w") as fo:
        fo.writelines(content_list)


def main():
    # 创建参数
    args = create_args()

    version = args.version
    force_cover = args.force_cover
    ic(force_cover)

    # 获取到表的信息
    table_info = connect_mysql_and_get_table_structure(args=args)

    # 通过 pwd 获取当前路径
    current_path = os.getcwd() + "/src/main/java/com/xiaojinzi/tallyserver"
    ic(current_path)

    createDaoEntityClass(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    createDtoEntityClass(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    createVoEntityClass(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    create_data_transform_file(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    createMapper(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    createService(
        current_path=current_path,
        table_info=table_info,
        force_cover=force_cover,
    )

    createController(
        current_path=current_path,
        table_info=table_info,
        version=version,
        force_cover=force_cover,
    )


if __name__ == "__main__":
    main()
