package io.github.tiagosilva110.Anya.controller.dto;

public record AccountCreateDTO(
        String name,
        String phone,
        String mail,
        String password_hash
) {


}