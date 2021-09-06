<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class LocationType extends Model
{
    use HasFactory;

    protected $fillable = [
        'type_name',
    ];

    public function location() : HasMany
    {
        return $this->hasMany(Location::class);
    }
}
