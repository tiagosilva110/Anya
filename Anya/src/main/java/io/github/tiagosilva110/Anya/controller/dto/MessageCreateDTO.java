package io.github.tiagosilva110.Anya.controller.dto;

import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.model.Contact;

import java.time.LocalDate;
import java.util.UUID;

public record MessageCreateDTO(
                       String contact,
                       String account,
                       String body
) {


//    public Autor mapearParaAutor(){
//        Autor autor = new Autor();
//        autor.setNome(this.nome);
//        autor.setDataNascimento(this.dataNascimento);
//        autor.setNacionalidade(this.nacionalidade);
//        return autor;
//    }
}