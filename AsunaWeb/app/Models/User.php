<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use HasFactory, Notifiable;

    protected $primaryKey = 'userID';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'guildMemberID',
        'locale',
        'timeZone',
        'themeID'
    ];

    /** The model's default values for attributes.
     *
     * @var array
     */
    protected $attributes = [
        'locale' => 'en_US',
        'timeZone' => 'UTC',
        'themeID' => 2,
        'isAdmin' => false
    ];
}
