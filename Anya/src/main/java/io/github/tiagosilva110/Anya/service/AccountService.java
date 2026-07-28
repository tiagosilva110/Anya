package io.github.tiagosilva110.Anya.service;

import io.github.tiagosilva110.Anya.model.Account;
import io.github.tiagosilva110.Anya.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AccountService {

    private final AccountRepository repository;

    public Account persist(Account account){
        return  repository.save(account);
    }

    public void update(Account account){
        if(account.getId() == null){
            throw new IllegalArgumentException("For update a account, it is necessary for it to be persisted");
        }
        repository.save(account);
    }

    public void delete(Account account){
        repository.delete(account);
    }

    public Optional<Account> findById(UUID id){
        return repository.findById(id);
    }
}
