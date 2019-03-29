<?php

namespace App;

use Illuminate\Notifications\Notifiable;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'eso_name', 'discord_id', 'authcode', 'role', 'guild_rank', 'password'
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];

    /**
     * The attributes that should be cast to native types.
     *
     * @var array
     */
    protected $casts = [
    ];

    /**
     * Generate an API session token.
     *
     * @return The generated token.
     */
    public function generateToken()
    {
      $this->api_token = str_random(60);
      $this->save();

      return $this->api_token;
    }

    /**
     * Invalidate the API session token.
     *
     * @return void
     */
     public function invalidateToken()
     {
       $this->api_token = null;
       $this->save();
     }

}
