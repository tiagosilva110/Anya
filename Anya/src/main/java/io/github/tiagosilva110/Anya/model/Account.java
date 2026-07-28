package io.github.tiagosilva110.Anya.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Table
@Entity
@Getter
@Setter
public class Account {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column
    private String name;

    @Column
    private String phone;

    @Column
    private String mail;

    @Column(name = "password_hash")
    private String passwordHash;

}
