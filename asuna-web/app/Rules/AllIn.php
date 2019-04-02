<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class AllIn implements Rule
{

  protected $array;

  public function __construct($array)
  {
      $this->array = $array;
  }

  /**
   * Determine if the validation rule passes.
   *
   * @param  string  $attribute
   * @param  mixed  $value
   * @return bool
   */
  public function passes($attribute, $value)
  {
      $elements = explode(',', $value);

      foreach($elements as $element) {
        if(!in_array($element, $this->array)){
          return false;
        }
      }
      return true;
  }

  /**
   * Get the validation error message.
   *
   * @return string
   */
  public function message()
  {
      return ':attribute contains an invalid value.';
  }
}
