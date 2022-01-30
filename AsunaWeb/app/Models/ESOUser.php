<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class ESOUser extends Model
{
    use HasFactory;

    protected $fillable = [
        'family_name'
    ];

    public function guilds() : BelongsToMany
    {
        return $this->belongsToMany(Guild::class);
    }

    public function guildMember() : BelongsToMany
    {
        return $this->belongsToMany(GuildMember::class);
    }
}
