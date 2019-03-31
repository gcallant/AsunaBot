<?php

namespace App\Http\Controllers;

use App\Event;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\Input;
use App\Traits\Filterable;

class EventsController extends Controller
{
    use Filterable;

    protected $resourceClass = Event::class;

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if (Gate::denies('create-event')) {
          return response()->json(['error' => 'Not authorized to create events.'], 403);
        }

        if (Gate::denies('proxy-create-event')) {
          $user = Auth::guard('api')->user();
          $request->request->set('created_by_id', $user->discord_id);
        }

        $validator = Validator::make($request->all(), [
          'event_name' => ['required', 'max:20'],
          'trial_name' => ['nullable', 'max:20'],
          'event_time' => ['required', 'date', 'after:now'],
          'created_by_id' => ['required'],
          'event_leader' => ['required', 'exists:users,discord_id'],
          'active' => ['nullable', 'boolean'],
          'description' => ['required', 'min:3', 'max:250'],
          'min_rank' => ['required'],
          'channel_info_message' => ['nullable'],
          'channel_id' => ['nullable'],
        ]);

        if($validator->fails()) {
          return response($validator->errors(), 400);
        }

        $event = Event::create($validator->validated());

        return response()->json(['event' => $event], 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show(Event $event)
    {
        return response()->json(['event' => $event], 200);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request Contains the updated fields
     * @param  \App\Event $event The current object in the database
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Event $event)
    {
      if (Gate::denies('edit-event', $event)) {
        return response()->json(['error' => 'Not authorized to update this event.'], 403);
      }

      $validator = Validator::make($request->all(), [
        'event_name' => ['max:20'],
        'trial_name' => ['max:20'],
        'event_time' => ['date', 'after:now'],
        'created_by_id' => ['exists:users,discord_id'],
        'event_leader' => ['exists:users,discord_id'],
        'active' => ['nullable', 'boolean'],
        'description' => ['min:3', 'max:250'],
        'min_rank' => ['string'],
        'channel_info_message' => ['nullable'],
        'channel_id' => ['nullable'],
      ]);

      if($validator->fails()) {
        return response($validator->errors(), 400);
      }

      $updatedEvent = $event->update($validator->validated());

      return response()->json(['event' => $event], 200);

    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
