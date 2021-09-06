<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class EventRoster extends Model
{
    use HasFactory;

    protected $fillable = [
        'max_tanks',
        'max_heals',
        'max_ranged_dps',
        'max_melee_dps'
    ];

    public function event() : BelongsTo
    {
        return $this->belongsTo(Event::class);
    }
}
