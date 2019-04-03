<?php

namespace App\Traits;

use Illuminate\Database\Eloquent\Model;

trait ControlsModel {

  public function resourceModel() {
    if (method_exists($this, 'resourceClass')) {
        return $this->resourceClass();
    }
    
    return property_exists($this, 'resourceClass') ? $this->resourceClass : Model::class;
  }
}
