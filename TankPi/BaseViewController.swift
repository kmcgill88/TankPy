//
//  BaseViewController.swift
//  TankPi
//
//  Created by Kevin McGill on 2/7/16.
//  Copyright © 2016 Kevin McGill. All rights reserved.
//

import Foundation
import UIKit

class BaseViewController : UIViewController {

    
    func showAlertWithMessage(title:String!, message:String!, action:UIAlertAction? ) {
        
        let alert = UIAlertController(title: title, message: message, preferredStyle: UIAlertControllerStyle.Alert)
        
        if action != nil {
            alert.addAction(action!)
        }
        
        self.presentViewController(alert, animated: true, completion: nil)
    }
    
    
    
}