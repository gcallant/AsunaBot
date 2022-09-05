package com.grantcallant.asunaspring.utility.helpers;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

/**
 * A collection of convenient stream methods.
 */
public class StreamHelper
{
  private StreamHelper(){}

  /**
   * Allows a generic mapping from a List of models to a list of DTOs or vice-versa.
   *
   * @param source      The source list to convert.
   * @param targetClass The class type to convert.
   * @param mapper      Since ModelMapper is defined as a Bean in our config, this should be Autowired eligible,
   *                    but in most cases you should have a mapper instance to inject into this method.
   * @param <S>         The source list type.
   * @param <T>         The target list type.
   * @return A converted/mapped list from type S to T.
   */
  public static <S, T> List<T> mapList(List<S> source, Class<T> targetClass, @Autowired ModelMapper mapper)
  {
    return source.stream().map(element -> mapper.map(element, targetClass)).toList();
  }
}
