plugins {
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dependency.management)
    alias(libs.plugins.flyway)
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.spring)
    alias(libs.plugins.kotlin.jpa)
    alias(libs.plugins.ben.manes.versions)
    idea
    java
}

group = "com.grantcallant"
version = "0.0.1-SNAPSHOT"
val queryDslVersion = "5.1.0"

repositories {
    mavenCentral()
}

// Fixed idea configuration
idea {
    module {
        sourceDirs.plusAssign(file("generated/"))
        generatedSourceDirs.plusAssign(file("generated/"))
    }
}

// Move clean task outside idea block
tasks.named("clean") {
    doFirst {
        delete(file("generated/"))
    }
}

/**
 * This allows us to run Flyway specific Gradle tasks independently of our application at runtime
 * IE having migrations run each time during application boot is not best practice.
 */
flyway {
    // Add null checks for environment variables
    driver = System.getenv("DB_DRIVER") ?: "org.postgresql.Driver"
    url = System.getenv("DB_URL") ?: "jdbc:postgresql://localhost:5432/asuna"
    user = System.getenv("DB_USER") ?: "postgres"
    password = System.getenv("DB_PASSWORD") ?: ""
    cleanDisabled = false
//    locations = arrayOf("filesystem:resources/db/migration")
}

java {
    sourceCompatibility = JavaVersion.VERSION_22
    targetCompatibility = JavaVersion.VERSION_22
}

// Configure Kotlin compilation
kotlin {
    jvmToolchain(22)
}

val mockitoAgent = configurations.create("mockitoAgent")

dependencies {
    implementation(libs.discord4j.core)
    implementation(libs.jackson.core) // Managed by Spring Boot BOM
    implementation(libs.flyway.core)
    implementation(libs.katharsis.spring)
    
    implementation(libs.jjwt.api)
    runtimeOnly(libs.jjwt.impl)
    runtimeOnly(libs.jjwt.jackson)
    
    implementation(libs.modelmapper)
    implementation(libs.spring.boot.starter.actuator)
    implementation(libs.spring.boot.starter.data.jpa) { exclude("org.apache.tomcat:tomcat-jdbc") }
    implementation(libs.spring.boot.starter.graphql)
    implementation(libs.spring.boot.starter.jdbc)
    implementation(libs.spring.boot.starter.oauth2.client)
    implementation(libs.spring.boot.starter.security)
    implementation(libs.spring.boot.starter.web)
    implementation(libs.spring.session.core)

    // Kotlin
    implementation(libs.kotlin.reflect)
    implementation(libs.kotlin.gradle.plugin)
    
    // Replace deprecated Springfox with SpringDoc OpenAPI
    implementation(libs.springdoc.openapi.starter.webmvc.ui)
    
    implementation(libs.streamex)
    implementation(libs.hikaricp)
    implementation(libs.jetbrains.annotations)

    compileOnly(libs.lombok)
    developmentOnly(libs.spring.boot.devtools)
    developmentOnly(libs.h2)
    runtimeOnly(libs.postgresql)

    // QueryDSL - Updated annotation processors for Jakarta
    implementation(libs.querydsl.core)
    implementation("com.querydsl:querydsl-jpa:${queryDslVersion}:jakarta")
    implementation(libs.querydsl.collections)
    annotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:jakarta")
    annotationProcessor(libs.spring.boot.configuration.processor)
    
    // Use only Jakarta annotations (removed javax dependencies)
    annotationProcessor(libs.jakarta.annotation.api)
    annotationProcessor(libs.jakarta.persistence.api)
    annotationProcessor(libs.lombok)

    // TEST
    testImplementation(libs.spring.boot.starter.test)
    testImplementation(libs.spring.webflux)
    testImplementation(libs.spring.graphql.test)
    testImplementation(libs.spring.security.test)
    testCompileOnly(libs.lombok)
    testAnnotationProcessor(libs.lombok)

    // Mockito Agent (Required for JVM 21+)
    // @see https://javadoc.io/static/org.mockito/mockito-core/5.19.0/org.mockito/org/mockito/Mockito.html#mockito-instrumentation
    testImplementation(libs.mockito)
    mockitoAgent(libs.mockito) { isTransitive = false }

    // QueryDSL for tests
    testImplementation(libs.querydsl.core)
    testImplementation("com.querydsl:querydsl-jpa:${queryDslVersion}:jakarta")
    testImplementation(libs.querydsl.collections)
    testAnnotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:jakarta")
    testAnnotationProcessor(libs.jakarta.annotation.api)
    testAnnotationProcessor(libs.jakarta.persistence.api)
}

val buildProfile: String? by project
apply(from = "profile-${buildProfile ?: "default"}.gradle.kts")

tasks {
    bootRun {
      args("--spring.profiles.active=local")
    }
    test {
        systemProperty("spring.profiles.active", "local")
        useJUnitPlatform()
        jvmArgs.add("-javaagent:${mockitoAgent.asPath}")
    }
}