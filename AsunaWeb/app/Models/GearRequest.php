<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class GearRequest extends Model
{
    use HasFactory;

    protected $fillable = [
        'guild_member_id',
        'gear_set_id'
    ];

    public function guildMember() : BelongsTo
    {
        return $this->belongsTo(GuildMember::class);
    }

    public function gearPiece() : BelongsToMany
    {
        return $this->belongsToMany(GearPiece::class);
    }

    public function gearSet() : BelongsTo
    {
        return $this->belongsTo(GearSet::class);
    }
}
