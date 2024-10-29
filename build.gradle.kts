import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    id("org.springframework.boot") version "3.0.5"
    id("io.spring.dependency-management") version "1.1.0"
    id("war")
    kotlin("jvm") version "1.7.22"
    kotlin("plugin.spring") version "1.7.22"
}

group = "com.xiaojinzi"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

war {
    webAppDirName = "tally"
}

repositories {
    mavenCentral()
    // 添加阿里的仓库
    // maven(url = "https://maven.aliyun.com/repository/public")
}

dependencies {
    // 引入 swagger
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.2.0")
    // compileOnly("jakarta.servlet:jakarta.servlet-api:6.0.0")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("com.auth0:java-jwt:3.19.1")
    implementation("org.aspectj:aspectjrt:1.9.9.1")
    implementation("org.aspectj:aspectjweaver:1.9.9.1")
    implementation("mysql:mysql-connector-java:8.0.30")
    implementation("com.baomidou:mybatis-plus-boot-starter:3.5.3")
    implementation("org.springframework.boot:spring-boot-starter-web") {
        // exclude(group = "org.springframework.boot", module ="spring-boot-starter-tomcat")
    }
    // compileOnly("org.springframework.boot:spring-boot-starter-tomcat")
    implementation("org.springframework.boot:spring-boot-starter-mail")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    // https://mvnrepository.com/artifact/com.google.code.gson/gson
    implementation("com.google.code.gson:gson:2.10.1")
    // 导入协程
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    // 导入 MybatisPlus
    implementation("com.baomidou:mybatis-plus-boot-starter:3.5.3")
    // 阿里发短信的
    implementation("com.aliyun:dysmsapi20170525:2.0.24")
    // 阿里 oss 的
    // implementation("com.aliyun.oss:aliyun-sdk-oss:3.17.2")
    // 阿里 sts 的
    // implementation("com.aliyun:alibabacloud-sts20150401:1.0.4")
    implementation("com.aliyun:sts20150401:1.1.4")
    // 阿里的 tea
    // implementation("com.aliyun:tea:1.2.9")
    implementation("com.alipay.sdk:alipay-sdk-java:4.39.37.ALL")
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xjsr305=strict")
        jvmTarget = "17"
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

springBoot {
    mainClass.set("com.xiaojinzi.tallyserver.TallyServerApplicationKt")
}
