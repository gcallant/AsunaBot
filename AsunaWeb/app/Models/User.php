<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use HasFactory, Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'guild_member_id',
        'locale',
        'time_zone',
        'theme_id'
    ];

    /** The model's default values for attributes.
     *
     * @var array
     */
    protected $attributes = [
        'locale' => 'en_US',
        'time_zone' => 'UTC',
        'theme_id' => 2,
        'is_admin' => false
    ];

    public function guildMember() : HasOne
    {
        return $this->hasOne(GuildMember::class);
    }

    public function theme() : BelongsTo
    {
        return $this->belongsTo(Theme::class);
    }
}
