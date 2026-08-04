package io.github.tiagosilva110.Anya.controller;

import io.github.tiagosilva110.Anya.controller.dto.AccountCreateDTO;
import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.service.AccountService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

@RestController
@RequestMapping("account")
@RequiredArgsConstructor
public class AccountController {

    private final AccountService service;

    @PostMapping
    public ResponseEntity<Object> create(@RequestBody AccountCreateDTO dto){

        Account account = new Account();

        account.setMail(dto.mail());
        account.setName(dto.name());
        account.setPhone(dto.phone());

        service.persist(account);
        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(account.getId())
                .toUri();

        return ResponseEntity.created(location).build();
    }

}
