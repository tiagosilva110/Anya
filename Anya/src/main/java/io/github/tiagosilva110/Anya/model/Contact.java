package io.github.tiagosilva110.Anya.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Table(name = "contact")
@Entity
@Getter
@Setter
public class Contact {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(
//            cascade = CascadeType.ALL, // faz um cascade para todas as operações no banco (Usar como estudo, não recomendado em produção)
            fetch = FetchType.LAZY
    )
    @JoinColumn(name = "account")
    private Account account;

    @Column
    private String name;

    @Column
    private String phone;

    @Column
    private String mail;

}
