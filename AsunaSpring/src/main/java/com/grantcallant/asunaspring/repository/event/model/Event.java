package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.guild.model.Guild;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;
import java.time.OffsetDateTime;
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
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @Column(name = "event_name", nullable = false, length = 200)
  private String eventName;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "event_type_id", nullable = false)
  private EventType eventType;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @OnDelete(action = OnDeleteAction.CASCADE)
  @JoinColumn(name = "guild_id", nullable = false)
  private Guild guild;

  @OneToOne(mappedBy = "event")
  private EventRoster eventRoster;

  @OneToOne(mappedBy = "event")
  private EventSignup eventSignup;

  @OneToOne(mappedBy = "event")
  private EventDatum eventDatum;
}
