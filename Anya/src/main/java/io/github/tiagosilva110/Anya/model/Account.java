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
    private String person;

    @Column
    private String email;

    @Column(name = "password_hash")
    private String passwordHash;

}
