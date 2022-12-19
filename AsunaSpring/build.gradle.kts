import org.codehaus.groovy.ast.tools.GeneralUtils.args

plugins {
    id("org.springframework.boot") version "2.7.4"
    id("io.spring.dependency-management") version "1.0.13.RELEASE"
    id("org.flywaydb.flyway") version "9.3.0"
    idea
    java
}

group = "com.grantcallant"
version = "0.0.1-SNAPSHOT"
var queryDslVersion = "5.0.0"
var lombokVersion = "1.18.24"

repositories {
    mavenCentral()
}

idea {
    module {
        sourceDirs.plusAssign(file("generated/"))
        generatedSourceDirs.plusAssign(file("generated/"))
    }
    tasks.named("clean") {
        delete(file("generated/"))
    }
}

/**
 * This allows us to run Flyway specific Gradle tasks independently of our application at runtime
 * IE having migrations run each time during application boot is not best practice.
 */
flyway {
    driver = System.getenv("DB_DRIVER")
    url = System.getenv("DB_URL")
    user = System.getenv("DB_USER")
    password = System.getenv("DB_PASSWORD")
    cleanDisabled = false
//    locations = arrayOf("filesystem:resources/db/migration")
}


java {
    sourceCompatibility = JavaVersion.VERSION_18
}



dependencies {
    implementation("com.discord4j:discord4j-core:3.2.3")
    implementation("com.fasterxml.jackson.core:jackson-core:2.14.0")
    implementation("org.flywaydb:flyway-core")
    implementation("io.jsonwebtoken:jjwt:0.9.1")
    implementation("org.modelmapper:modelmapper:3.1.1")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa") { exclude("org.apache.tomcat:tomcat-jdbc") }
    implementation("org.springframework.boot:spring-boot-starter-graphql")
    implementation("org.springframework.boot:spring-boot-starter-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-oauth2-client")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.security:spring-security-jwt:1.1.1.RELEASE")
    implementation("org.springframework.session:spring-session-core")
    implementation("io.springfox:springfox-boot-starter:3.0.0")
    implementation("io.springfox:springfox-swagger-ui:3.0.0")
    implementation("one.util:streamex:0.8.1")
    implementation("com.zaxxer:HikariCP")

    compileOnly("org.projectlombok:lombok:${lombokVersion}")
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    developmentOnly("com.h2database:h2")
    runtimeOnly("org.postgresql:postgresql")

    // QueryDSL
    implementation("com.querydsl:querydsl-core:${queryDslVersion}")
    implementation("com.querydsl:querydsl-jpa:${queryDslVersion}")
    implementation("com.querydsl:querydsl-collections:${queryDslVersion}")
    annotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:general")
    annotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:jpa")
    annotationProcessor("org.springframework.boot", "spring-boot-starter-data-jpa")
    annotationProcessor("javax.annotation", "javax.annotation-api", "1.3.2")
    annotationProcessor("org.hibernate.javax.persistence", "hibernate-jpa-2.1-api", "1.0.2.Final")
    annotationProcessor("jakarta.annotation:jakarta.annotation-api") // This prevents java.lang.NoClassDefFoundError
    annotationProcessor("jakarta.persistence:jakarta.persistence-api") // This prevents java.lang.NoClassDefFoundError

    annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
    annotationProcessor("org.projectlombok:lombok:${lombokVersion}")

    // TEST
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework:spring-webflux")
    testImplementation("org.springframework.graphql:spring-graphql-test")
    testImplementation("org.springframework.security:spring-security-test")
    testCompileOnly("org.projectlombok:lombok:${lombokVersion}")
    testAnnotationProcessor("org.projectlombok:lombok:${lombokVersion}")

    // QueryDSL
    testImplementation("com.querydsl:querydsl-core:${queryDslVersion}")
    testImplementation("com.querydsl:querydsl-jpa:${queryDslVersion}")
    testImplementation("com.querydsl:querydsl-collections:${queryDslVersion}")
    testAnnotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:general")
    testAnnotationProcessor("com.querydsl:querydsl-apt:${queryDslVersion}:jpa")
    testAnnotationProcessor("org.springframework.boot", "spring-boot-starter-data-jpa")
    testAnnotationProcessor("javax.annotation", "javax.annotation-api", "1.3.2")
    testAnnotationProcessor("org.hibernate.javax.persistence", "hibernate-jpa-2.1-api", "1.0.2.Final")
    testAnnotationProcessor("jakarta.annotation:jakarta.annotation-api") // This prevents java.lang.NoClassDefFoundError
    testAnnotationProcessor("jakarta.persistence:jakarta.persistence-api") // This prevents java.lang.NoClassDefFoundError
}

val buildProfile: String? by project
apply(from = "profile-${buildProfile ?: "default"}.gradle.kts")

tasks.getByName<Test>("test") {
    systemProperty("spring.profiles.active", "local")
    useJUnitPlatform()
}

tasks.named("build") {
    args("--spring.profiles.active=local")
}
