package io.github.tiagosilva110.Anya.repository;

import io.github.tiagosilva110.Anya.model.Message;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface MessageRepository extends JpaRepository<Message, UUID> {
    Message findById(String id);
}
