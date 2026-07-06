package io.github.tiagosilva110.Anya.configuration;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

@Configuration
public class DatabaseConfiguration {

    @Value("${spring.datasource.url}")
    String url;
    @Value("${spring.datasource.username}")
    String username;
    @Value("${spring.datasource.password}")
    String password;
    @Value("${spring.datasource.driver-class-name}")
    String driver;

    //RECOMENDADO PELA EQUIPE SPRING, PERMITE SETAR POOL DE CONEXÕES
    @Bean
    public DataSource hikariDataSource(){

        HikariConfig config = new HikariConfig();
        config.setUsername(username);
        config.setPassword(password);
        config.setDriverClassName(driver);
        config.setJdbcUrl(url);

        config.setMaximumPoolSize(10);
        config.setMinimumIdle(1);
        config.setPoolName("library-db-pool");
        config.setMaxLifetime(600000); // 600 mil ms (10 minutos)
        config.setConnectionTimeout(100000); // timeout para tentar nova conexão
        config.setConnectionTestQuery("select 1"); // query de teste

        return new HikariDataSource(config);
    }
}
