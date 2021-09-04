<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GuildMember extends Model
{
    use HasFactory;

    public $incrementing = false;
    protected $primaryKey = 'guildMemberID';
    protected $fillable = [
        'guildMemberID',
        'name',
        'discordUserID',
        'discordRoleIDs'
    ];
}