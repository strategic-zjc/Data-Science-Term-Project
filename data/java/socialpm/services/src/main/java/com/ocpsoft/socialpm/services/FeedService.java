/**
 * This file is part of OCPsoft SocialPM: Agile Project Management Tools (SocialPM) 
 *
 * Copyright (c)2011 Lincoln Baxter, III <lincoln@ocpsoft.com> (OCPsoft)
 * Copyright (c)2011 OCPsoft.com (http://ocpsoft.com)
 * 
 * If you are developing and distributing open source applications under 
 * the GNU General Public License (GPL), then you are free to re-distribute SocialPM 
 * under the terms of the GPL, as follows:
 *
 * SocialPM is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SocialPM is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SocialPM.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * For individuals or entities who wish to use SocialPM privately, or
 * internally, the following terms do not apply:
 *  
 * For OEMs, ISVs, and VARs who wish to distribute SocialPM with their 
 * products, or host their product online, OCPsoft provides flexible 
 * OEM commercial licenses.
 * 
 * Optionally, Customers may choose a Commercial License. For additional 
 * details, contact an OCPsoft representative (sales@ocpsoft.com)
 */

package com.ocpsoft.socialpm.services;

import java.util.Date;
import java.util.List;

import javax.ejb.TransactionAttribute;
import javax.enterprise.event.Observes;
import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;

import com.ocpsoft.socialpm.model.feed.FeedEvent;
import com.ocpsoft.socialpm.model.project.Project;
import com.ocpsoft.socialpm.model.user.Profile;

@TransactionAttribute
public class FeedService extends PersistenceUtil
{
   private static final long serialVersionUID = 5716926734835352145L;

   @Override
   public void setEntityManager(EntityManager em)
   {
      this.em = em;
   }

   public void addEvent(@Observes final FeedEvent event)
   {
      event.setCreatedOn(new Date());
      create(event);
   }

   public List<FeedEvent> list(final int limit, final int offset)
   {
      TypedQuery<FeedEvent> query = em.createNamedQuery("feedEvent.all", FeedEvent.class)
               .setFirstResult(offset);

      if (limit > 0)
      {
         query.setMaxResults(limit);
      }

      return query.getResultList();
   }

   public List<FeedEvent> listByProfile(final Profile profile, final int limit, final int offset)
   {
      TypedQuery<FeedEvent> query = em.createNamedQuery("feedEvent.byUser", FeedEvent.class)
               .setParameter("user", profile)
               .setFirstResult(offset);

      if (limit > 0)
      {
         query.setMaxResults(limit);
      }

      return query.getResultList();
   }

   public List<FeedEvent> listByProject(final Project p, final int limit, final int offset)
   {
      return findByNamedQuery("feedItem.byProject", p);
   }
}
