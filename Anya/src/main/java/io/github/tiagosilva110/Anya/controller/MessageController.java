package io.github.tiagosilva110.Anya.controller;


import io.github.tiagosilva110.Anya.controller.dto.MessageCreateDTO;
import io.github.tiagosilva110.Anya.controller.mapper.MessageMapper;
import io.github.tiagosilva110.Anya.model.Message;
import io.github.tiagosilva110.Anya.service.MessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
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
    private final MessageMapper mapper;
    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/start-recording")
    public ResponseEntity<Void> startRecording() {
        String pythonUrl = "http://localhost:5000/start";

        try {
            restTemplate.postForEntity(pythonUrl, null, String.class);

            return ResponseEntity.accepted().build();
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @PostMapping
    public ResponseEntity<Void> save(@RequestBody MessageCreateDTO dto){
        Message message = mapper.toEntity(dto);
        service.persist(message);
        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(message.getId())
                .toUri();

        return ResponseEntity.created(location).build();

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
