package io.github.tiagosilva110.Anya.controller;

import io.github.tiagosilva110.Anya.controller.dto.AccountCreateDTO;
import io.github.tiagosilva110.Anya.controller.dto.ContactCreateDTO;
import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.model.Contact;
import io.github.tiagosilva110.Anya.service.AccountService;
import io.github.tiagosilva110.Anya.service.ContactService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("contact")
@RequiredArgsConstructor
public class ContactController {

    private final ContactService service;
    private final AccountService accountService;

    @PostMapping
    public ResponseEntity<Object> create(@RequestBody ContactCreateDTO dto){

        Contact contact = new Contact();

        contact.setMail(dto.mail());
        contact.setName(dto.name());
        contact.setPhone(dto.phone());

        Optional<Account> account = accountService.findById(UUID.fromString(dto.account()));


        if(account.isPresent()){
            contact.setAccount(account.get());

            service.persist(contact);
            URI location = ServletUriComponentsBuilder
                    .fromCurrentRequest()
                    .path("/{id}")
                    .buildAndExpand(contact.getId())
                    .toUri();

            return ResponseEntity.created(location).build();
        } else{
            return ResponseEntity.unprocessableContent().build();
        }

    }

}