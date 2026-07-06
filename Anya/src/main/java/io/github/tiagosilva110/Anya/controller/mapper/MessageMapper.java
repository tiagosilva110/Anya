package io.github.tiagosilva110.Anya.controller.mapper;

import io.github.tiagosilva110.Anya.controller.dto.MessageCreateDTO;
import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.model.Message;
import org.mapstruct.Mapper;

import java.util.UUID;

@Mapper(componentModel = "spring")
public interface MessageMapper {

    //@Mapping(source = "nome", target = "autor") // Propriedades com nome diferente
    //@Mapping(source = "dataNascimento", target = "nascimento")
    //@Mapping(source = "nacionalidade", target = "origem")
    Message toEntity(MessageCreateDTO dto);

    default Account map(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }

        Account account = new Account();

        // Se o ID na sua classe Account for do tipo UUID:
        account.setId(UUID.fromString(value));

        // OBSERVAÇÃO: Se o ID na sua classe Account for String,
        // comente a linha do UUID acima e use a linha abaixo:
        // account.setId(value);

        return account;
    }
}