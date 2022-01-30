<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class GearSet extends Model
{
    use HasFactory;

    protected $fillable = [
        'gear_set_name',
        'location_id'
    ];

    public function gearRequest() : HasMany
    {
        return $this->hasMany(GearRequest::class);
    }
}
