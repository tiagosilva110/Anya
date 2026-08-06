package io.github.tiagosilva110.Anya.controller;


import io.github.tiagosilva110.Anya.controller.dto.MessageCreateDTO;
import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.model.Contact;
import io.github.tiagosilva110.Anya.model.Message;
import io.github.tiagosilva110.Anya.service.AccountService;
import io.github.tiagosilva110.Anya.service.ContactService;
import io.github.tiagosilva110.Anya.service.MessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("message")
@RequiredArgsConstructor
public class MessageController {

    private final MessageService service;
    private final AccountService accountService;
    private final ContactService contactService;

    private final RestTemplate restTemplate = new RestTemplate();


    @PostMapping
    public ResponseEntity<Object> create(@RequestBody MessageCreateDTO dto) {
        Message message = new Message();
        Optional<Account> account = accountService.findById(UUID.fromString(dto.account()));
        if (account.isPresent()) {
            message.setAccount(account.get());

            String phone = dto.phone();
            Optional<Contact> contact = contactService.findByPhoneAndAccount(phone, account.get());

            if (contact.isPresent()) {
                message.setContact(contact.get());
            }
            message.setBody(dto.body());
            service.persist(message);
            URI location = ServletUriComponentsBuilder
                        .fromCurrentRequest()
                        .path("/{id}")
                        .buildAndExpand(message.getId())
                        .toUri();

            return ResponseEntity.created(location).body(message);
        } else {
            return ResponseEntity.unprocessableContent().build();
        }
    }

    @DeleteMapping
    public ResponseEntity<Void> delete(@RequestParam String idString){
        Optional<Message> message = service.findById(UUID.fromString(idString));
        if (message.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        service.delete(message.get());
        return ResponseEntity.noContent().build();

    }

}
