package io.github.tiagosilva110.Anya.service;

import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.model.Contact;
import io.github.tiagosilva110.Anya.repository.ContactRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ContactService {

    private final ContactRepository repository;

    public Contact persist(Contact contact){
        return  repository.save(contact);
    }

    public void update(Contact contact){
        if(contact.getId() == null){
            throw new IllegalArgumentException("For update a contact, it is necessary for it to be persisted");
        }
        repository.save(contact);
    }

    public void delete(Contact contact){
        repository.delete(contact);
    }

    public Optional<Contact> findById(UUID id){
        return repository.findById(id);
    }

    public Optional<Contact> findByPhoneAndAccount(String phone, Account account){
        return repository.findByPhoneAndAccount(phone, account);
    }
}
