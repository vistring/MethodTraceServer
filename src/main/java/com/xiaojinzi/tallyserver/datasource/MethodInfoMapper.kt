package com.xiaojinzi.tallyserver.datasource

import com.baomidou.mybatisplus.core.mapper.BaseMapper
import com.xiaojinzi.tallyserver.domain.MethodGroupInfoDo
import com.xiaojinzi.tallyserver.domain.MethodInfoDo
import org.apache.ibatis.annotations.Mapper
import org.apache.ibatis.annotations.Param
import org.apache.ibatis.annotations.Select

@Mapper
interface MethodInfoMapper : BaseMapper<MethodInfoDo> {

    /*
        SELECT
            method_full_name,
            MIN(method_cost) as min_method_cost,
            MAX(method_cost) as max_method_cost,
            MIN(method_total_cost) as min_method_total_cost,
            MAX(method_total_cost) as max_method_total_cost,
            AVG(method_cost) as avg_method_cost,
            AVG(method_total_cost) as avg_method_total_cost
        FROM method_trace where app_id = 1
        GROUP BY method_full_name_md5, method_full_name
     */
    @Select(
        value = [
            "SELECT method_full_name, method_full_name_md5, MIN(method_cost) as min_method_cost, MAX(method_cost) as max_method_cost, MIN(method_total_cost) as min_method_total_cost, MAX(method_total_cost) as max_method_total_cost, AVG(method_cost) as avg_method_cost, AVG(method_total_cost) as avg_method_total_cost, COUNT(method_full_name_md5) as count FROM method_trace where app_id = \${app_id} GROUP BY method_full_name_md5, method_full_name ORDER BY avg_method_cost DESC, avg_method_total_cost DESC, count DESC limit \${page_start}, \${page_size}"
        ]
    )
    fun selectGroupList(
        @Param("app_id") appId: Int,
        @Param("page_start") pageStart: Int,
        @Param("page_size") pageSize: Int = 10,
    ): List<MethodGroupInfoDo>

}