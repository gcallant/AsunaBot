package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.guild.model.Guild;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

/**
 * The model for events.
 */
@Getter
@Setter
@Entity
@Table(name = "events")
public class Event
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @Column(nullable = false, length = 200)
  private String eventName;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(nullable = false)
  private EventType eventType;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @OnDelete(action = OnDeleteAction.CASCADE)
  @JoinColumn(nullable = false)
  private Guild guild;

  @OneToOne(fetch = FetchType.LAZY, mappedBy = "event")
  private EventRoster eventRoster;

  @OneToOne(fetch = FetchType.LAZY, mappedBy = "event")
  private EventSignup eventSignup;

  @OneToOne(fetch = FetchType.LAZY, mappedBy = "event")
  private EventDatum eventDatum;

}
