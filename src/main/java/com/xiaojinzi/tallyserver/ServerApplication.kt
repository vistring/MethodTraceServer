package com.xiaojinzi.tallyserver

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.builder.SpringApplicationBuilder
import org.springframework.boot.runApplication
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer
import org.springframework.context.annotation.EnableAspectJAutoProxy
import org.springframework.scheduling.annotation.EnableScheduling

@EnableScheduling
@EnableAspectJAutoProxy
@SpringBootApplication
class ServerApplication : SpringBootServletInitializer() {

    override fun configure(builder: SpringApplicationBuilder): SpringApplicationBuilder {
        return builder.sources(
            ServerApplication::class.java,
        )
    }

}

fun main(args: Array<String>) {
    runApplication<ServerApplication>(*args)
}
