package io.github.tiagosilva110.Anya.model;

import jakarta.persistence.*;
import lombok.Generated;
import lombok.Getter;
import lombok.Setter;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.UUID;

@Table(name = "message")
@Entity
@Getter
@Setter
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(
//            cascade = CascadeType.ALL, // faz um cascade para todas as operações no banco (Usar como estudo, não recomendado em produção)
            fetch = FetchType.LAZY
    )
    @JoinColumn(name = "contact")
    private Contact contact;

    @ManyToOne(
//            cascade = CascadeType.ALL, // faz um cascade para todas as operações no banco (Usar como estudo, não recomendado em produção)
            fetch = FetchType.LAZY
    )
    @JoinColumn(name = "account")
    private Account account;

    @Column
    private String body;

    @Column
    private byte[] voice;

    @Column
    private String transcription;

    @Column(name = "created", insertable = false, updatable = false)
    private LocalDateTime created;


}
