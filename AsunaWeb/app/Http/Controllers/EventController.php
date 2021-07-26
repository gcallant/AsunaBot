<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;

class EventController extends Controller
{
    public function makeEvent(event)
    {
        $event = Event::create(event);

        return new JsonResponse($event, 200);
    }
}
