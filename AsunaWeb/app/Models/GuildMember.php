<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class GuildMember extends Model
{
    use HasFactory;

    public $incrementing = false;
    protected $fillable = [
        'id',
        'name',
        'discord_user_id',
        'discord_role_ids'
    ];

    public function guild(): BelongsToMany
    {
        return $this->belongsToMany(Guild::class);
    }
}
