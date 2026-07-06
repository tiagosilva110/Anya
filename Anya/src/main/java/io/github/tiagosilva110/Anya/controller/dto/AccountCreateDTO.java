package io.github.tiagosilva110.Anya.controller.dto;

public record AccountCreateDTO(
        String person,
        String email,
        String password_hash
) {


//    public Autor mapearParaAutor(){
//        Autor autor = new Autor();
//        autor.setNome(this.nome);
//        autor.setDataNascimento(this.dataNascimento);
//        autor.setNacionalidade(this.nacionalidade);
//        return autor;
//    }
}