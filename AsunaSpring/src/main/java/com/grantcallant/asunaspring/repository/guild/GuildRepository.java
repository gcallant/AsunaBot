package com.grantcallant.asunaspring.repository.guild;

import com.grantcallant.asunaspring.repository.guild.model.Guild;
import org.springframework.data.querydsl.QuerydslPredicateExecutor;
import org.springframework.data.repository.PagingAndSortingRepository;

import java.util.UUID;

public interface GuildRepository extends PagingAndSortingRepository<Guild, UUID>, QuerydslPredicateExecutor<Guild>
{
}
