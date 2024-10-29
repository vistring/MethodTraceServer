package com.xiaojinzi.tallyserver.domain

import com.baomidou.mybatisplus.annotation.IdType
import com.baomidou.mybatisplus.annotation.TableField
import com.baomidou.mybatisplus.annotation.TableId
import com.baomidou.mybatisplus.annotation.TableName
import com.xiaojinzi.tallyserver.util.md5

fun Int.toAppString(): String {
    return when (this) {
        1 -> "Blink"
        2 -> "Magpie"
        3 -> "VSMethodTraceDemo"
        else -> "Unknown"
    }
}

fun String.toAppId(): Int {
    return when (this) {
        "Blink" -> 1
        "Magpie" -> 2
        "VSMethodTraceDemo" -> 3
        else -> 0
    }
}

@TableName("method_trace")
data class MethodInfoDo(
    @TableId(type = IdType.AUTO)
    val id: Long? = null,
    @TableField("app_id")
    val appId: Int? = null,
    @TableField("method_cost")
    val methodCost: Long? = null,
    @TableField("method_total_cost")
    val methodTotalCost: Long? = null,
    @TableField("method_full_name")
    val methodFullName: String? = null,
    @TableField("method_full_name_md5")
    val methodFullNameMd5: String? = methodFullName?.md5(),
    // ; 隔开的
    @TableField("stack_trace_str")
    val stackTraceStr: String? = null,
)

@TableName("method_trace")
data class MethodGroupInfoDo(
    @TableField("method_full_name")
    val methodFullName: String,
    @TableField("method_full_name_md5")
    val methodFullNameMd5: String,
    @TableField("min_method_cost")
    val minMethodCost: Long,
    @TableField("max_method_cost")
    val maxMethodCost: Long,
    @TableField("min_method_total_cost")
    val minMethodTotalCost: Long,
    @TableField("max_method_total_cost")
    val maxMethodTotalCost: Long,
    @TableField("avg_method_cost")
    val avgMethodCost: Long,
    @TableField("avg_method_total_cost")
    val avgMethodTotalCost: Long,
    @TableField("count")
    val count: Int,
)

data class MethodInfoVo(
    val id: Long,
    val appId: String,
    val methodCost: Long,
    val methodTotalCost: Long,
    val methodFullName: String,
    // ; 隔开的
    val stackTraceStr: String,
)

data class MethodGroupInfoVo(
    val methodFullName: String,
    val methodFullNameMd5: String,
    val minMethodCost: Long,
    val maxMethodCost: Long,
    val minMethodTotalCost: Long,
    val maxMethodTotalCost: Long,
    val avgMethodCost: Long,
    val avgMethodTotalCost: Long,
    val count: Int,
)

fun MethodInfoDo.toMethodInfoVo(): MethodInfoVo {
    return MethodInfoVo(
        id = id!!,
        appId = appId!!.toAppString(),
        methodCost = methodCost!!,
        methodTotalCost = methodTotalCost!!,
        methodFullName = methodFullName!!,
        stackTraceStr = stackTraceStr!!,
    )
}

fun MethodGroupInfoDo.toMethodGroupInfoVo(): MethodGroupInfoVo {
    return MethodGroupInfoVo(
        methodFullName = methodFullName,
        methodFullNameMd5 = methodFullNameMd5,
        minMethodCost = minMethodCost,
        maxMethodCost = maxMethodCost,
        minMethodTotalCost = minMethodTotalCost,
        maxMethodTotalCost = maxMethodTotalCost,
        avgMethodCost = avgMethodCost,
        avgMethodTotalCost = avgMethodTotalCost,
        count = count,
    )
}
