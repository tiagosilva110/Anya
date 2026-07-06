package io.github.tiagosilva110.Anya.controller.dto;

import java.time.LocalDate;
import java.util.UUID;

public record MessageCreateDTO(
                       String sender,
                       String body,
                       String account
) {


//    public Autor mapearParaAutor(){
//        Autor autor = new Autor();
//        autor.setNome(this.nome);
//        autor.setDataNascimento(this.dataNascimento);
//        autor.setNacionalidade(this.nacionalidade);
//        return autor;
//    }
}