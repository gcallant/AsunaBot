package com.grantcallant.asunaspring.repository.event;

import com.grantcallant.asunaspring.repository.event.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.querydsl.QuerydslPredicateExecutor;

import java.util.UUID;

/**
 * Manages the DAO layer for events.
 */
public interface EventRepository extends JpaRepository<Event, UUID>, QuerydslPredicateExecutor<Event>
{
}
