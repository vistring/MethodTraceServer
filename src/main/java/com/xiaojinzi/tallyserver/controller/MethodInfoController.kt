package com.xiaojinzi.tallyserver.controller

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper
import com.xiaojinzi.tallyserver.datasource.MethodInfoMapper
import com.xiaojinzi.tallyserver.domain.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*
import retrofit2.http.GET

@RestController
class MethodInfoController {

    @Autowired
    lateinit var methodInfoMapper: MethodInfoMapper

    @PostMapping("add")
    @ResponseStatus(code = HttpStatus.OK)
    fun add(
        appId: String,
        methodCost: Long,
        methodTotalCost: Long,
        methodFullName: String,
        stackTraceStr: String,
    ): MethodInfoVo? {
        val targetDo = MethodInfoDo(
            appId = appId.toAppId(),
            methodCost = methodCost,
            methodTotalCost = methodTotalCost,
            methodFullName = methodFullName,
            stackTraceStr = stackTraceStr,
        )
        methodInfoMapper.insert(
            targetDo
        )
        return targetDo.toMethodInfoVo()
    }

    @GetMapping("list")
    @ResponseStatus(code = HttpStatus.OK)
    fun listByApp(
        appId: String,
        @RequestParam(required = true) pageNumber: Int,
        @RequestParam(required = false) pageSize: Int? = null,
    ): List<MethodGroupInfoVo> {

        if (pageNumber < 1) {
            throw IllegalArgumentException("pageNumber must be greater than 0")
        }

        /*SELECT
            MIN(method_cost) as min_method_cost,
            MAX(method_cost) as max_method_cost,
            MIN(method_total_cost) as min_method_total_cost,
            MAX(method_total_cost) as max_method_total_cost,
            AVG(method_cost) as avg_method_cost,
            AVG(method_total_cost) as avg_method_total_cost
        FROM method_trace where app_id = 1
        GROUP BY method_full_name_md5*/

        val finalPageSize = (pageSize ?: 10).coerceIn(minimumValue = 1, maximumValue = 100)

        return methodInfoMapper.selectGroupList(
            appId = appId.toAppId(),
            pageStart = finalPageSize * (pageNumber - 1),
            pageSize = finalPageSize,
        ).map { it.toMethodGroupInfoVo() }
    }

    @GetMapping("detail")
    @ResponseStatus(code = HttpStatus.OK)
    fun getMethodInfo(
        appId: String,
        methodFullNameMd5: String,
    ): MethodInfoVo {
        return methodInfoMapper.selectOne(
            QueryWrapper<MethodInfoDo>().apply {
                this.eq("app_id", appId.toAppId())
                this.eq("method_full_name_md5", methodFullNameMd5)
                this.last("limit 1")
            }
        ).toMethodInfoVo()
    }

}