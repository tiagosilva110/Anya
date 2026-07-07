package io.github.tiagosilva110.Anya.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Table(name = "temp_messages")
@Entity
@Getter
@Setter
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column
    private String sender;

    @Column
    private String body;

    @ManyToOne(
//            cascade = CascadeType.ALL, // faz um cascade para todas as operações no banco (Usar como estudo, não recomendado em produção)
            fetch = FetchType.LAZY
    )
    @JoinColumn(name = "account")
    private Account account;

}
