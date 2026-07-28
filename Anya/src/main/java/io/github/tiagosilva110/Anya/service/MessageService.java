package io.github.tiagosilva110.Anya.service;

import io.github.tiagosilva110.Anya.model.Message;
import io.github.tiagosilva110.Anya.repository.MessageRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class MessageService {

    private final MessageRepository repository;

    public Message persist(Message message) {
        return repository.save(message);
    }

    public void update(Message message){
        if(message.getId() == null){
            throw new IllegalArgumentException("For update a message, it is necessary for it to be persisted");
        }
        repository.save(message);
    }

    public void delete(Message message){
        repository.delete(message);
    }

    public Optional<Message> findById(UUID id){
        return repository.findById(id);
    }
}
