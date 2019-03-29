<?php

namespace App\Http\Controllers\Auth;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Auth\Events\Registered;
use App\User;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Foundation\Auth\RegistersUsers;

class RegisterController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | Register Controller
    |--------------------------------------------------------------------------
    |
    | This controller handles the registration of new users as well as their
    | validation and creation. By default this controller uses a trait to
    | provide this functionality without requiring any additional code.
    |
    */

    use RegistersUsers;

    /**
     * Where to redirect users after registration.
     *
     * @var string
     */
    protected $redirectTo = '/home';

    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('guest');
    }

    /**
     * Get a validator for an incoming registration request.
     *
     * @param  array  $data
     * @return \Illuminate\Contracts\Validation\Validator
     */
    protected function validator(array $data)
    {
        return Validator::make($data, [
            'eso_name' => ['required', 'string', 'max:255', 'unique:users'],
            'discord_id' => ['required', 'string', 'max:255', 'unique:users'],
            'guild_rank' => ['required', 'string', 'max:255'],
            'authcode' => ['required', 'string', 'min:8', 'unique:users'],
        ]);
    }

    /**
     * Create a new user instance after a valid registration.
     *
     * @param  array  $data
     * @return \App\User
     */
    protected function create(array $data)
    {
        return User::create([
            'eso_name' => $data['eso_name'],
            'discord_id' => $data['discord_id'],
            'guild_rank' => $data['guild_rank'],
            'authcode' => $data['authcode'],
            // Every user's "password" is FAKE_PASSWORD.
            // It is never used, but must exist or errors will occur.
            'password' => Hash::make("FAKE_PASSWORD"),
            'role' => 'MEMBER',
        ]);
    }

    /**
     * Handle a registration request for the application.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    protected function register(Request $request)
    {
        $authcode = $this->generateAuthCode();
        $request->request->set('authcode', hash('sha256', $authcode));

        $validator = $this->validator($request->all());

        if($validator->fails()) {
          // User already exists.
          return response($validator->errors(), 409);
        }

        event(new Registered($user = $this->create($request->all())));

        // Replace hashed authcode with plaintext to return to users.
        // Hashed representation is still in database.
        $user->authcode = $authcode;

        return $this->registered($request, $user);
    }

    /**
     * The user has been registered.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  mixed  $user
     * @return mixed
     */
    protected function registered(Request $request, $user)
    {
        return response()->json(['data' => $user->toArray()], 201);
    }

    /**
    * Generate a random 12 character auth code for user login.
    *
    * @return The generated authcode.
    */
    public function generateAuthCode()
    {
      return str_random(4) . '-' . str_random(4) . '-' . str_random(4);
    }
}
