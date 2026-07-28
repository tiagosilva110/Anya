package io.github.tiagosilva110.Anya.controller;


import io.github.tiagosilva110.Anya.controller.dto.MessageCreateDTO;
import io.github.tiagosilva110.Anya.controller.mapper.MessageMapper;
import io.github.tiagosilva110.Anya.model.Message;
import io.github.tiagosilva110.Anya.service.MessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("message")
@RequiredArgsConstructor
public class MessageController {

    private final MessageService service;
    private final MessageMapper mapper;
    private final RestTemplate restTemplate = new RestTemplate();


    @PostMapping
    public ResponseEntity<MessageReturnDTO> startRecording(@RequestBody MessageCreateDTO dto) {
        Message message = mapper.toEntity(dto);
        service.persist(message);
        String pythonUrl = "http://localhost:5000/start";


        try {
            ResponseEntity<MessageReturnDTO> response = restTemplate.postForEntity(pythonUrl, dto, MessageReturnDTO.class);
            return ResponseEntity.accepted().body(response.getBody());
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }

//    @PostMapping
//        public ResponseEntity<Void> save(@RequestBody MessageCreateDTO dto){
//            Message message = mapper.toEntity(dto);
//            service.persist(message);
//            URI location = ServletUriComponentsBuilder
//                    .fromCurrentRequest()
//                    .path("/{id}")
//                    .buildAndExpand(message.getId())
//                    .toUri();
//
//            return ResponseEntity.created(location).build();
//
//    }

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
