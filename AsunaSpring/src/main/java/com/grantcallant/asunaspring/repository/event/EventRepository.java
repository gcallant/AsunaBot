package com.grantcallant.asunaspring.repository.event;

import com.grantcallant.asunaspring.repository.event.model.Event;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.List;


/**
 * Manages the DAO layer for events.
 */
@Service
@Transactional(propagation = Propagation.REQUIRED)
public class EventRepository
{
  @PersistenceContext
  private EntityManager entityManager;


  public List<Event> getAllEvents()
  {
    //TODO: Actually query data to return
    Query query = entityManager.createNativeQuery("SELECT e.name, e.id, e.details from events;");
    return (List<Event>) query.getResultList();
  }
}
