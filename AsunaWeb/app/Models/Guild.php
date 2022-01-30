<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Guild extends Model
{
    use HasFactory;

    public $incrementing = false;
    protected $attributes = [
        'time_zone' => 'UTC'
    ];

    protected $fillable = [
        'guild_id',
        'time_zone',
        'guild_name'
    ];

    public function guildMember() : BelongsToMany
    {
        return $this->belongsToMany(GuildMember::class);
    }
}
