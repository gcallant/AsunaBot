<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Event extends Model
{
    use HasFactory;

    protected $fillable = [
        'event_name',
        'event_type_id',
        'guild_id'
    ];

    public function eventType() : BelongsTo
    {
        return $this->belongsTo(EventType::class);
    }

    public function eventData() : HasOne
    {
        return $this->hasOne(EventData::class);
    }

    public function eventSignup() : HasMany
    {
        return $this->hasMany(EventSignup::class);
    }

    public function eventRoster() : HasOne
    {
        return $this->hasOne(EventRoster::class);
    }
}
