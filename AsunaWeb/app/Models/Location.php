<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Location extends Model
{
    use HasFactory;

    protected $fillable = [
        'location_name',
        'location_type_id'
    ];

    public function locationType() : BelongsTo
    {
        return $this->belongsTo(LocationType::class);
    }
}
