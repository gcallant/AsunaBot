plugins {
    id("org.springframework.boot") version "2.7.3"
    id("io.spring.dependency-management") version "1.0.13.RELEASE"
    id("org.flywaydb.flyway") version "9.3.0"
    java
}

group = "com.grantcallant"
version = "0.0.1-SNAPSHOT"

repositories {
    mavenCentral()
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
    cleanDisabled = true
//    locations = arrayOf("filesystem:resources/db/migration")
}


java {
    sourceCompatibility = JavaVersion.VERSION_18
}



dependencies {
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa") {exclude("org.apache.tomcat:tomcat-jdbc")}
    implementation("org.springframework.boot:spring-boot-starter-graphql")
    implementation("org.springframework.boot:spring-boot-starter-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-oauth2-client")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.session:spring-session-core")
    implementation("org.springframework.security:spring-security-jwt:1.1.1.RELEASE")
    implementation("io.springfox:springfox-boot-starter:3.0.0")
    implementation("io.springfox:springfox-swagger-ui:3.0.0")
    implementation("one.util:streamex:0.8.1")
    implementation("io.jsonwebtoken:jjwt:0.9.1")
    implementation("com.fasterxml.jackson.core:jackson-core:2.13.4")
    implementation("org.modelmapper:modelmapper:3.1.0")
    implementation("com.zaxxer:HikariCP")
    compileOnly("org.projectlombok:lombok")
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    implementation("org.flywaydb:flyway-core")
    developmentOnly("com.h2database:h2")
    runtimeOnly("org.postgresql:postgresql")
    runtimeOnly("org.mariadb.jdbc:mariadb-java-client")
    annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
    annotationProcessor("org.projectlombok:lombok")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework:spring-webflux")
    testImplementation("org.springframework.graphql:spring-graphql-test")
    testImplementation("org.springframework.security:spring-security-test")
}

val buildProfile: String? by project
apply(from = "profile-${buildProfile ?: "default"}.gradle.kts")

tasks.getByName<Test>("test") {
    systemProperty("spring.profiles.active", "test")
    useJUnitPlatform()
}
