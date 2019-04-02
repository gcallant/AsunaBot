<?php
use Illuminate\Validation\Rule;
use App\Rules\AllIn;

return [
  "isValidAppRole" => Rule::in(array_keys(config('enums.appRoles'))),
  "isValidSignupRole" => Rule::in(array_keys(config('enums.signupRoles'))),
  "allValidSignupRoles" => new AllIn(array_keys(config('enums.signupRoles'))),
];
