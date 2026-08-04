package io.github.tiagosilva110.Anya.controller.dto;

public record ContactCreateDTO (
        String name,
        String phone,
        String mail,
        String account
){
}
